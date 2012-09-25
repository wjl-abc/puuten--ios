//
//  LibViewController.m
//  puuten
//
//  Created by wang jialei on 12-8-17.
//
//

#import "LibViewController.h"
#import "ImageViewCell.h"
#import "WBViewController.h"
#import "BSHeader.h"

@interface LibViewController ()

@end

@implementation LibViewController
@synthesize categ = _categ;
@synthesize type = _type;

- (void)setCateg:(NSString *)categ{
    _categ = categ;
}

- (void)setType:(NSString *)type{
    _type = type;
}

- (void)prepareForSegue:(UIStoryboardSegue *)segue sender:(id)sender
{
    
    if ([segue.identifier isEqualToString:@"details"]){
        WBViewController *wb = (WBViewController *)segue.destinationViewController;
        wb.wb_id=selected_cell;
        wb.order = selected_order;
        wb.arrayData = array4wb;
        wb.dicData = dic4wb;
    }
}

- (void)didReceiveMemoryWarning
{
    // Releases the view if it doesn't have a superview.
    [super didReceiveMemoryWarning];
    
    // Release any cached data, images, etc that aren't in use.
}

#pragma mark - View lifecycle

- (void)loadInternetData {
    NSURL *nsURL = [[NSURL alloc] initWithString:URL];
    NSURL *libURL = [NSURL URLWithString:@"/home/event_lib/" relativeToURL:nsURL];
    ASIFormDataRequest *_request=[ASIFormDataRequest requestWithURL:libURL];
    __weak ASIFormDataRequest *request = _request;
    [request setPostValue:@"ios" forKey:@"mobile"];
    [request setPostValue:_categ forKey:@"class"];
    [request setPostValue:_type forKey:@"type"];
    [request setCompletionBlock:^{
        NSData *responseData = [request responseData];
        NSError* error;
        //NSMutableArray* json = [NSJSONSerialization JSONObjectWithData:responseData options:kNilOptions error:&error];
        NSMutableDictionary* json = [NSJSONSerialization JSONObjectWithData:responseData options:kNilOptions error:&error];
        arrayData = [json objectForKey:@"data"];
        for( int i=0 ; i<[arrayData count]; i++){
            NSDictionary* instance = [[NSDictionary alloc] init];
            instance = [arrayData objectAtIndex:i];
            NSURL *img_url = [[NSURL alloc] initWithString:[instance objectForKey:@"thumbnail_pic"]];
            NSData *data = [[NSData alloc] initWithContentsOfURL:img_url];
            UIImage *image = [[UIImage alloc] initWithData:data];
            NSMutableDictionary* ele4wb = [[NSMutableDictionary alloc] init];
            [ele4wb setValue:image forKey:@"image"];
            [ele4wb setValue:[instance objectForKey:@"ratio"] forKey:@"ratio"];
            [ele4wb setValue:[instance objectForKey:@"body"] forKey:@"body"];
            [ele4wb setValue:[instance objectForKey:@"bs_avatar"] forKey:@"bs_avatar"];
            [ele4wb setValue:[instance objectForKey:@"name"] forKey:@"name"];
            
            [array4wb addObject:ele4wb];
        }
        [dic4wb setValue:array4wb forKey:@"data"];
        [dic4wb setValue:[json objectForKey:@"len"] forKey:@"len"];
        [dic4wb setValue:libURL forKey:@"URL"];
        
        [self dataSourceDidLoad];
    }];
    [request setFailedBlock:^{
        [self dataSourceDidError];
    }];
    
    [request startAsynchronous];
    
}

- (void)dataSourceDidLoad {
    [waterFlow reloadData];
}

- (void)dataSourceDidError {
    [waterFlow reloadData];
}

- (void)viewDidLoad
{
    [super viewDidLoad];
	self.title = _categ;
}

-(void)loadMore{
    
    [arrayData addObjectsFromArray:arrayData];
    [waterFlow reloadData];
}

#pragma mark WaterFlowViewDataSource
- (NSInteger)numberOfColumsInWaterFlowView:(WaterFlowView *)waterFlowView{
    
    return 2;
}

- (NSInteger)numberOfAllWaterFlowView:(WaterFlowView *)waterFlowView{
    
    return [arrayData count];
}

- (UIView *)waterFlowView:(WaterFlowView *)waterFlowView cellForRowAtIndexPath:(IndexPath *)indexPath{
    
    ImageViewCell *view = [[ImageViewCell alloc] initWithIdentifier:nil];
    
    return view;
}


-(void)waterFlowView:(WaterFlowView *)waterFlowView  relayoutCellSubview:(UIView *)view withIndexPath:(IndexPath *)indexPath{
    
    //arrIndex是某个数据在总数组中的索引
    int arrIndex = indexPath.row * waterFlowView.columnCount + indexPath.column;
    
    
    NSDictionary *object = [arrayData objectAtIndex:arrIndex];
    
    //NSURL *nsURL = [[NSURL alloc] initWithString:[object objectForKey:@"thumbnail_pic"]];
    int wb_id = [[object objectForKey:@"wb_id"] intValue];
    ImageViewCell *imageViewCell = (ImageViewCell *)view;
    imageViewCell.indexPath = indexPath;
    imageViewCell.columnCount = waterFlowView.columnCount;
    imageViewCell.tt=1;
    [imageViewCell relayoutViews];
    //NSData *data = [[NSData alloc] initWithContentsOfURL:nsURL];
    //UIImage *image = [[UIImage alloc] initWithData:data];
    //[arrayImg addObject:image];
    [(ImageViewCell *)view setImageWithImg:[[array4wb objectAtIndex:arrIndex] objectForKey:@"image"] withWB_ID:wb_id withOrder:arrIndex withBS:@"mmmm" withType:0 withDelegate:self];
}


#pragma mark WaterFlowViewDelegate
- (CGFloat)waterFlowView:(WaterFlowView *)waterFlowView heightForRowAtIndexPath:(IndexPath *)indexPath{
    
    int arrIndex = indexPath.row * waterFlowView.columnCount + indexPath.column;
    NSDictionary *dict = [arrayData objectAtIndex:arrIndex];
    float height_width_ratio = [[dict objectForKey:@"ratio"] floatValue];
    return waterFlowView.cellWidth*height_width_ratio;
}

- (void)waterFlowView:(WaterFlowView *)waterFlowView didSelectRowAtIndexPath:(IndexPath *)indexPath{
    
    NSLog(@"indexpath row == %d,column == %d",indexPath.row,indexPath.column);
}

- (void)viewDidUnload
{
    [super viewDidUnload];
//    [array4wb release];
    
    array4wb = nil;
    arrayData = nil;
    dic4wb = nil;
    dicData = nil;
    waterFlow = nil;
     
    // Release any retained subviews of the main view.
}
- (void)viewDidAppear:(BOOL)animated
{
    arrayData = [[NSMutableArray alloc] init];
    array4wb = [[NSMutableArray alloc] init];
    dic4wb = [[NSMutableDictionary alloc] init];
    self.navigationItem.rightBarButtonItem = [[UIBarButtonItem alloc] initWithTitle:@"More" style:UIBarButtonItemStyleBordered target:self action:@selector(loadMore)];
        
    waterFlow = [[WaterFlowView alloc] initWithFrame:CGRectMake(0, 0, 320, 460-44)];
    waterFlow.waterFlowViewDelegate = self;
    waterFlow.waterFlowViewDatasource = self;
    waterFlow.backgroundColor = [UIColor whiteColor];
    
    [self.view addSubview:waterFlow];
        //[waterFlow release];
    [self loadInternetData];
    [super viewDidAppear:animated];
    
}

- (void)viewWillAppear:(BOOL)animated
{
    self.navigationController.navigationBar.barStyle = UIBarStyleDefault;
    //self.parentViewController.tabBarController.tabBar.hidden  = NO;
    [super viewWillAppear:animated];
}

- (BOOL)shouldAutorotateToInterfaceOrientation:(UIInterfaceOrientation)interfaceOrientation
{
    return (interfaceOrientation != UIInterfaceOrientationPortraitUpsideDown);
}


- (void)imageViewCell:(ImageViewCell *)sender
          clickedCell:(int)cell_id
         clickedOrder:(int)cell_order
{
    selected_cell = cell_id;
    selected_order = cell_order;
    [self performSegueWithIdentifier:@"details" sender:self];
}



@end

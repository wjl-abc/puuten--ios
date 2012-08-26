//
//  LibViewController.m
//  puuten
//
//  Created by wang jialei on 12-8-17.
//
//

#import "LibViewController.h"
#import "LoginViewController.h"
#import "ImageViewCell.h"
#import "WBViewController.h"
#import "BSHeader.h"

@interface LibViewController ()

@end

@implementation LibViewController

- (void)prepareForSegue:(UIStoryboardSegue *)segue sender:(id)sender
{
    
    if ([segue.identifier isEqualToString:@"details"]){
        WBViewController *wb = (WBViewController *)segue.destinationViewController;
        wb.wb_id=selected_cell;
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
    [request setCompletionBlock:^{
        NSData *responseData = [request responseData];
        NSError* error;
        NSDictionary* json = [NSJSONSerialization JSONObjectWithData:responseData options:kNilOptions error:&error];
        arrayData = json;
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
	
}

-(void)loadMore{
    
    [arrayData addObjectsFromArray:arrayData];
    [waterFlow reloadData];
}

#pragma mark WaterFlowViewDataSource
- (NSInteger)numberOfColumsInWaterFlowView:(WaterFlowView *)waterFlowView{
    
    return 3;
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
    
    NSURL *nsURL = [[NSURL alloc] initWithString:[object objectForKey:@"thumbnail_pic"]];
    int wb_id = [[object objectForKey:@"wb_id"] intValue];
    ImageViewCell *imageViewCell = (ImageViewCell *)view;
    imageViewCell.indexPath = indexPath;
    imageViewCell.columnCount = waterFlowView.columnCount;
    imageViewCell.tt=1;
    [imageViewCell relayoutViews];
    [(ImageViewCell *)view setImageWithURL:nsURL withWB_ID:wb_id withBS:@"mmmm" withType:0 withDelegate:self];
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
    // Release any retained subviews of the main view.
}
- (void)viewDidAppear:(BOOL)animated
{
    arrayData = [[NSMutableArray alloc] init];
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

- (BOOL)shouldAutorotateToInterfaceOrientation:(UIInterfaceOrientation)interfaceOrientation
{
    return (interfaceOrientation != UIInterfaceOrientationPortraitUpsideDown);
}


- (void)imageViewCell:(ImageViewCell *)sender
          clickedCell:(int)cell_id
{
    selected_cell = cell_id;
    [self performSegueWithIdentifier:@"details" sender:self];
}



@end

//
//  ProfileViewController.m
//  puuten
//
//  Created by wang jialei on 12-8-26.
//
//

#import "ProfileViewController.h"
#import "LoginViewController.h"
#import "ImageViewCell.h"
#import "WBViewController.h"
#import "BSHeader.h"

@interface ProfileViewController ()

@end

@implementation ProfileViewController


- (void)didReceiveMemoryWarning
{
    // Releases the view if it doesn't have a superview.
    [super didReceiveMemoryWarning];
    
    // Release any cached data, images, etc that aren't in use.
}

#pragma mark - View lifecycle

- (void)loadInternetData {
    NSURL *nsURL = [[NSURL alloc] initWithString:URL];
    //NSURL *libURL = [NSURL URLWithString:@"/wishing_list/" relativeToURL:nsURL];
    NSURL *libURL = [NSURL URLWithString:@"/wat/your_buzz/" relativeToURL:nsURL];
    ASIFormDataRequest *_request=[ASIFormDataRequest requestWithURL:libURL];
    __weak ASIFormDataRequest *request = _request;
    [request setPostValue:@"ios" forKey:@"mobile"];
    [request setCompletionBlock:^{
        NSData *responseData = [request responseData];
        NSError* error;
        NSDictionary* json = [NSJSONSerialization JSONObjectWithData:responseData options:kNilOptions error:&error];
        arrayData = json;
        [testData addObject:arrayData];
        [testData addObject:arrayData];
        [self dataSourceDidLoad];
    }];
    [request setFailedBlock:^{
        [self dataSourceDidError];
    }];
    
    [request startAsynchronous];
    
}

- (void)dataSourceDidLoad {
    [waterFlow_wat reloadData];
    [waterFlow_wish reloadData];
}

- (void)dataSourceDidError {
    [waterFlow_wat reloadData];
    [waterFlow_wish reloadData];
}

- (IBAction)click1:(id)sender {
    waterFlow_wat.frame = CGRectMake(0, 100, 320, 460-100-44);
    waterFlow_wish.frame = CGRectZero;
}

- (IBAction)click2:(id)sender {
    waterFlow_wish.frame = CGRectMake(0, 100, 320, 460-100-44);
    waterFlow_wat.frame = CGRectZero;
}

- (void)viewDidLoad
{
    [super viewDidLoad];
	
}
/*
-(void)loadMore{
    
    [arrayData addObjectsFromArray:arrayData];
    [waterFlow_wat reloadData];
}*/

#pragma mark WaterFlowViewDataSource
- (NSInteger)numberOfColumsInWaterFlowView:(WaterFlowView *)waterFlowView{
    if (waterFlowView.tag) {
        return 2;
    }
    else
        return 3;
}

- (NSInteger)numberOfAllWaterFlowView:(WaterFlowView *)waterFlowView{
    if([testData count])
        return [[testData objectAtIndex:waterFlowView.tag] count];
    else
        return 0;
    
}

- (UIView *)waterFlowView:(WaterFlowView *)waterFlowView cellForRowAtIndexPath:(IndexPath *)indexPath{
    
    ImageViewCell *view = [[ImageViewCell alloc] initWithIdentifier:nil];
    
    return view;
}


-(void)waterFlowView:(WaterFlowView *)waterFlowView  relayoutCellSubview:(UIView *)view withIndexPath:(IndexPath *)indexPath{
    
    //arrIndex是某个数据在总数组中的索引
    int arrIndex = indexPath.row * waterFlowView.columnCount + indexPath.column;
    
    NSMutableArray *test = [testData objectAtIndex:0];
    NSDictionary *object = [test objectAtIndex:arrIndex];
    
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
    testData = [[NSMutableArray alloc] initWithCapacity:2];
    for (int i=0; i<[testData count]; i++) {
        NSMutableArray *test = [[NSMutableArray alloc] init];
        [testData addObject:test];
    }
   // self.navigationItem.rightBarButtonItem = [[UIBarButtonItem alloc] initWithTitle:@"More" style:UIBarButtonItemStyleBordered target:self action:@selector(loadMore)];
    
    waterFlow_wat = [[WaterFlowView alloc] initWithFrame:CGRectMake(0, 70, 320, 460-44-70)];
    waterFlow_wat.waterFlowViewDelegate = self;
    waterFlow_wat.waterFlowViewDatasource = self;
    waterFlow_wat.tag = 0;
    waterFlow_wat.backgroundColor = [UIColor whiteColor];
    
     waterFlow_wish = [[WaterFlowView alloc] initWithFrame:CGRectMake(0, 70, 320, 460-44-70)];
     waterFlow_wish.waterFlowViewDelegate = self;
     waterFlow_wish.waterFlowViewDatasource = self;
     waterFlow_wish.tag = 1;
     waterFlow_wish.backgroundColor = [UIColor whiteColor];
     
    [self.view addSubview:waterFlow_wat];
    [self.view addSubview:waterFlow_wish];
    
    [self loadInternetData];
    
    [super viewDidAppear:animated];
}

- (BOOL)shouldAutorotateToInterfaceOrientation:(UIInterfaceOrientation)interfaceOrientation
{
    return (interfaceOrientation != UIInterfaceOrientationPortraitUpsideDown);
}


@end
